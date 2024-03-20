from dataclasses import dataclass
from urllib.request import urlopen, Request
import sys
import json
import logging
import subprocess
import asyncio

@dataclass
class PackageData:
    name: str
    json_data: str = ""
    version_current: str = "-"
    version_new: str = ""

class PipHelper:
    def install(package_name, callback):
        PipHelper.run_pip_async(
            f"install-package-{package_name}",
            ["install", "--user", package_name],
            callback)

    def update(package_name, callback):
        PipHelper.run_pip_async(
            f"update-package-{package_name}",
            ["install", "-U", "--user", package_name],
            callback)

    def uninstall(package_name, callback):
        PipHelper.run_pip_async(
            f"uninstall-package-{package_name}",
            ["uninstall", "-y", package_name],
            callback)

    def run_pip_async(task_name, args_list, callback_func):
        if taskMgr.hasTaskNamed(task_name):
            base.messenger.send(
                "FRAME_show_warning",
                ["This process is already running"])
            return
        task = taskMgr.add(PipHelper.check_pip_done_task, task_name)
        task.proc = subprocess.Popen(
            [sys.executable, "-m", "pip"] + args_list,
            stdout=subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        task.callback_func = callback_func

    def check_pip_done_task(task):
        if task.proc.poll() is None:
            return task.cont
        if task.proc.poll() == 0:
            if task.proc.stderr:
                stderr = task.proc.stderr.read()
        if stderr:
            logging.error(stderr.decode())
        task.callback_func()
        return task.done


    def __init__(self):
        self.package_names = []
        self.package_data = {}

    def add_package(self, package_name):
        self.package_names.append(package_name)

    def load_packages(self, installed_callback, outdated_callback):
        for package_name in self.package_names:
            self.refresh_package_data(package_name)

        self.installed_callback = installed_callback
        self.outdated_callback = outdated_callback

        self.get_installed_packages()

    def refresh_package_data(self, package_name):
        pd = self.__get_package_data(package_name)
        self.package_data[package_name] = pd

    def get_installed_packages(self):
        self.__get_pip_output_as_list_runner(
            "get-installed-packages-task",
            ["list"],
            self.__got_installed_callback)

    def get_outdated_packages(self):
        outdated_packages = {}
        for package_name, pd in self.package_data.items():
            if pd.version_new.strip() != pd.version_current.strip() \
            and pd.version_current != "-":
                outdated_packages[package_name] = pd
        self.outdated_callback(outdated_packages)

    def __got_installed_callback(self, value):
        installed_packages = {}
        for package in value:
            filtered_list = self.__get_filtered_pip_data(package)
            # Check if the entry has the desired number of parts
            if len(filtered_list) < 2:
                continue
            # add the package data
            if filtered_list[0] not in self.package_data.keys():
                continue
            self.package_data[filtered_list[0]].version_current = filtered_list[1]
            installed_packages[filtered_list[0]] = self.package_data[filtered_list[0]]

        self.installed_callback(installed_packages)
        self.get_outdated_packages()

    def __get_package_data(self, package_name):
        pd = PackageData(package_name)
        req = Request(
            f"https://pypi.org/pypi/{pd.name}/json",
            method='GET')
        logging.debug(f"Get package data of {pd.name}")
        try:
            with urlopen(req) as response:
                response_content = response.read()
                pd.json_data = json.loads(response_content)
                pd.version_new = pd.json_data["info"]["version"]
        except Exception as e:
            logging.exception(f"Failed to get data for package {pd.name}")
        return pd

    def __get_filtered_pip_data(self, package_string):
        # split by spaces
        package_data_list = package_string.split(" ")
        # remove empty parts in the list
        filtered_list = list(filter(None, package_data_list))
        # Check if the entry has the desired number of parts
        return filtered_list

    def __get_pip_output_as_list_runner(self, task_name, args_list, callback_func):
        if taskMgr.hasTaskNamed(task_name):
            return
        task = taskMgr.add(self.__get_pip_output_as_list_task, task_name)
        task.proc = subprocess.Popen(
            [sys.executable, "-m", "pip"] + args_list,
            stdout=subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        task.callback_func = callback_func

    def __get_pip_output_as_list_task(self, task):
        if task.proc.poll() is None:
            return task.cont
        if task.proc.poll() == 0:
            if task.proc.stdout:
                stdout = task.proc.stdout.read()
            if task.proc.stderr:
                stderr = task.proc.stderr.read()
        ret_list = []
        if stdout:
            ret_list = stdout.decode().split("\n")[2:]
        if stderr:
            logging.error(stderr.decode())
        task.callback_func(ret_list)
        return task.done
