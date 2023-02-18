import asyncio
import copy
import logging
from typing import Awaitable, Dict, Hashable, List, Tuple, Union

import aiohttp
import requests

from . import parsing
from .entities import PackageBase, PackageVariant, PackageVersion

__all__ = ["package_search_match", "generate_download_url"]


QUERY_URL: str = "https://www.apkmirror.com"
QUERY_PARAMS: Dict[str, str] = {
    "post_type": "app_release",
    "searchtype": "apk",
    "s": "",
    "minapi": "true",
}
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5"
        " (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5 "
    )
}
FILE_ENDINGS = {"BUNDLE": "apkm", "APK": "apk"}
logger = logging.getLogger(__name__)


def gather_from_dict(tasks: Dict[Hashable, Awaitable], return_exceptions=False):
    # results = await asyncio.gather(
    #     *tasks.values(), loop=loop, return_exceptions=return_exceptions
    # )
    return tasks
    # return dict(zip(tasks.keys(), results))


def _generate_params_list(packages: List[str]) -> List[str]:
    param_list = []
    for package in packages:
        params = copy.copy(QUERY_PARAMS)
        params["s"] = package
        param_list.append(params)
    return param_list


def package_search(packages: List[str]) -> Dict[str, PackageBase]:
    """Entrypoint for performing the search async"""
    search_results = execute_package_search(packages)
    package_defs = parsing.process_search_result(search_results)
    logger.debug("Packages found: %s", ",".join(list(package_defs.keys())))
    release_defs = execute_release_info(package_defs)
    parsing.process_release_result(release_defs)
    variant_defs = execute_variant_info(package_defs)
    parsing.process_variant_result(variant_defs)
    return package_defs


def package_search_match(package_url: List[str], versions: List[str]) -> PackageBase:
    """Perform a targeted search on a root page

    :param package_url: URL to the package
    :param version: Version string to process
    """
    package_defs = execute_package_page([package_url])
    package_name = list(package_defs.keys())[0]
    for pkg_version in list(package_defs[package_name].versions.keys())[:]:
        if pkg_version not in versions:
            del package_defs[package_name].versions[pkg_version]
    if len(package_defs[package_name].versions) != len(versions):
        diff = set(versions).difference(set(package_defs[package_name].versions))
        raise RuntimeError("{} is missing {}".format(package_name, diff))
    release_defs = execute_release_info(package_defs)
    parsing.process_release_result(release_defs)
    return package_defs[package_name]


def generate_download_url(variant: PackageVariant) -> str:
    """Generates a packages temporary download URL

    :param variant: Variant to determine URL
    """
    results = _perform_basic_query([variant.variant_info])
    variant_defs = {variant: results[0]}
    parsing.process_variant_result(variant_defs)
    results = _perform_basic_query([variant.variant_download_page])
    download_results = {variant: results[0]}
    parsing.process_variant_download_result(download_results)
    return variant.download_url


def execute_package_search(packages: List[str]) -> List[str]:
    """Perform aiohttp requests to APKMirror

    :param list packages: Packages that will be searched for. Each package will generate a new
        request

    :return: A list of results containing the first page of each package search
    :rtype: list
    """
    param_list: List[str] = _generate_params_list(packages)
    return _perform_search(param_list)


def execute_package_page(packages: List[str]) -> Dict[str, PackageBase]:
    """Query all root package pages

    :param packages: List of root package pages to query
    """
    results = _perform_basic_query(packages)
    return parsing.process_package_page(results)


def execute_release_info(packages: Dict[str, PackageBase]) -> Dict[PackageVersion, str]:
    """Execute all requests related to the package versions

    :param dict package_defs: Current found information from the initial search. It will be updated
        in place with the release information found during the step
    """
    releases = []
    for info in packages.values():
        for package_version in info.versions.values():
            releases.append(package_version)
    return _perform_dict_lookup(releases)


def execute_variant_info(packages: Dict[str, PackageBase]) -> Dict[PackageVersion, str]:
    variants = []
    for info in packages.values():
        for package_version in info.versions.values():
            for arch in package_version.arch.values():
                variants.extend(arch)
    return _perform_dict_lookup(variants)


def gather_release_info(
    releases: List[PackageBase],
) -> Tuple[PackageVersion, PackageVariant, str]:

    results = _perform_dict_lookup(releases)
    return results


def _fetch_one(url, params):
    return requests.get(url=url, params=params, headers=HEADERS).text


def _perform_search(query_params: List[str]):
    results = [_fetch_one(QUERY_URL, param) for param in query_params]
    return results


def _perform_basic_query(urls: List[str]):
    required_urls = [_fetch_one(url, {}) for url in urls]

    return required_urls


def _perform_dict_lookup(requests: List[Union[PackageVersion, PackageVariant]]):
    if len(requests) == 0:
        return []
    if type(requests[0]) == PackageVersion:
        identifier = "releases"
        url_attr = "link"
    else:
        identifier = "variants"
        url_attr = "variant_download_page"

    tasks = {}
    logger.info("About to query %s %s", len(requests), identifier)
    for request in requests:
        url = getattr(request, url_attr)
        if url:
            tasks[request] = _fetch_one(getattr(request, url_attr), {})
    results = gather_from_dict(tasks)
    return results


def resp_to_dict(resp):
    goal = {}
    for key, values in resp.items():
        versions_dict = {}
        versions = values.versions
        for key2, values2 in versions.items():
            arch_dict = {}
            arch_info = values2.arch
            for key3, values3 in arch_info.items():
                arch_infos = [
                    {
                        "apk_type": value4.apk_type,
                        "download_url": value4.download_url,
                        "variant_download_page": value4.variant_download_page,
                        "variant_info": value4.variant_info,
                        "dpi": value4.dpi,
                        "version_code": value4.version_code,
                        "package": value4.package,
                    }
                    for value4 in values3
                ]
                arch_dict[key3] = arch_infos

            versions_dict[key2] = {"link": values2.link, "arch": arch_dict}
        goal[key] = {
            "title": values.title,
            "package_name": values.package_name,
            "info_page": values.info_page,
            "versions": versions_dict,
        }
    return goal


async def download_file_async(url, type, file_name):
    file_ending = FILE_ENDINGS[type]
    filename = f"{file_name}.{file_ending}"
    data: bytearray = bytearray()
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=2400)
    ) as session:
        async with session.get(
            url,
            headers=HEADERS,
            allow_redirects=True,
        ) as resp:
            while True:
                chunk = await resp.content.read(4096)
                if not chunk:
                    break
                data += bytearray(chunk)
    if not data:
        print("got no data")
    open(f"downloads/{filename}", "wb").write(data)
    return filename


def download_file(url, type, file_name):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(
        download_file_async(
            url=url,
            type=type,
            file_name=file_name,
        )
    )


# download_file(
#     url="https://apkmirror.com/wp-content/themes/APKMirror/download.php?id=4456170&key=840006b07762174d2421c97fd63f09daf31e2a34",
#     type="APK",
#     file_name="test",
# )
