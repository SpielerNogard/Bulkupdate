from __future__ import print_function, unicode_literals

import os
from typing import Dict, List

from .device_manager import DeviceManager
from .entities import PackageBase, PackageVariant, PackageVersion
from .search import download_file, generate_download_url, package_search
from .ui import UI


class BulkUpdate:
    def __init__(self):
        self._check_for_download_folders()

        self._ui = UI()
        self._device_manager = DeviceManager()

        found_files = self._find_installable_files()

        file_name = self._ui._show_list_of_options(
            name="installable_files",
            choices=found_files,
            message="Which file do you want to install?",
            append_options=["Download from APKMirror"],
        )
        if file_name == "Download from APKMirror":
            resp = self._search_with_apk_mirror()
            file_name = f"downloads/{self._select_package_version(resp=resp)}"

        devices = self._device_manager.get_list_of_devices()
        selected_devices = self._ui._show_multi_select(
            name="devices",
            choices=devices,
            message="Please select all devices on which the app should be installed",
        )
        print(selected_devices)
        failed_devices = []
        for device in selected_devices:
            installed = self._device_manager.install_app(device, file_name)
            if not installed:
                failed_devices.append(device)
        if failed_devices:
            print(f"The following devices failed the install")
            for failed_device in failed_devices:
                print(f"{failed_device} \n")

    def _select_package_version(self, resp: Dict[str, PackageBase]):
        download_urls = {}
        options = []
        for key, value in resp.items():
            versions: Dict[str, PackageVersion] = value.versions
            for version_key, version_value in versions.items():
                archs: Dict[str, List[PackageVariant]] = version_value.arch
                for arch_key, arch_value in archs.items():
                    for arch in arch_value:
                        apk_type = arch.apk_type
                        version_code = arch.version_code

                        option_key = (
                            f"{key} {version_key} {arch_key} {version_code} {apk_type}"
                        )
                        options.append(option_key)
                        download_urls[option_key] = {
                            "url": generate_download_url(variant=arch),
                            "type": apk_type,
                            "file_name": option_key.replace(" ", "_"),
                        }
        option = self._ui._show_list_of_options(
            name="apks",
            choices=options,
            message="Please choose the apk/bundle that should be downloaded: ",
        )
        print("The download will now start")
        file_name = download_file(**download_urls[option])
        print(f"downloaded file: {file_name}")
        return file_name

    def _search_with_apk_mirror(self):
        packages = self._ui._user_input(
            name="package", message="What package should be searched on APKMirror?"
        )
        print(f"Searching {packages} on APKMirror, this could take a while.")
        resp = package_search([packages])
        return resp

    def _find_installable_files(self):
        found_files = []
        found_files.extend(self._search_for_already_existing_apks())
        found_files.extend(self._search_for_already_existing_bundles())
        return found_files

    def _check_for_download_folders(self):
        path = "downloads"
        if not os.path.exists(path):
            os.makedirs(path)

    def _search_for_file_ending(self, file_ending):
        found_files = []
        for file in os.listdir("downloads"):
            if file.endswith(file_ending):
                found_files.append(os.path.join("downloads", file))
        return found_files

    def _search_for_already_existing_apks(self):
        found_files = self._search_for_file_ending("apk")
        return found_files

    def _search_for_already_existing_bundles(self):
        found_files = self._search_for_file_ending("apks")
        return found_files
