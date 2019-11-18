# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define COMPONENT storage_local_static_provisioner
%define RPM_NAME caas-%{COMPONENT}
%define RPM_MAJOR_VERSION 2.3.3
%define RPM_MINOR_VERSION 1
%define go_version 1.12.9
%define IMAGE_TAG %{RPM_MAJOR_VERSION}-%{RPM_MINOR_VERSION}
%define docker_build_dir %{_builddir}/%{RPM_NAME}-%{RPM_MAJOR_VERSION}/docker-build
%define docker_save_dir %{_builddir}/%{RPM_NAME}-%{RPM_MAJOR_VERSION}/docker-save

Name:           %{RPM_NAME}
Version:        %{RPM_MAJOR_VERSION}
Release:        %{RPM_MINOR_VERSION}%{?dist}
Summary:        Containers as a Service %{COMPONENT} component
License:        %{_platform_license} and GNU General Public License v2.0 only and MIT license and BSD 3-clause New or Revised License and MIT License and Curl License and BSD
URL:            https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner
BuildArch:      %{_arch}
Vendor:         %{_platform_vendor} and kubernetes-sigs/sig-storage-local-static-provisioner unmodified
Source0:        %{name}-%{version}.tar.gz

Requires: docker-ce >= 18.09.2, rsync
BuildRequires: docker-ce-cli >= 18.09.2, xz

%description
This rpm contains the storage local static provisioner container for caas subsystem.

%prep
%autosetup

%build
docker build \
  --network=host \
  --no-cache \
  --force-rm \
  --build-arg HTTP_PROXY="${http_proxy}" \
  --build-arg HTTPS_PROXY="${https_proxy}" \
  --build-arg NO_PROXY="${no_proxy}" \
  --build-arg http_proxy="${http_proxy}" \
  --build-arg https_proxy="${https_proxy}" \
  --build-arg no_proxy="${no_proxy}" \
  --build-arg STORAGE_LOCAL_STATIC_PROVISIONER_VERSION="%{version}" \
  --build-arg go_version="%{go_version}" \
  --tag %{COMPONENT}:%{IMAGE_TAG} \
  %{docker_build_dir}/%{COMPONENT}/
mkdir -p %{docker_save_dir}/
docker save %{COMPONENT}:%{IMAGE_TAG} | xz -z -T2 > %{docker_save_dir}/%{COMPONENT}:%{IMAGE_TAG}.tar
docker rmi %{COMPONENT}:%{IMAGE_TAG}

%install
mkdir -p %{buildroot}/%{_caas_container_tar_path}
rsync -av %{docker_save_dir}/%{COMPONENT}:%{IMAGE_TAG}.tar %{buildroot}/%{_caas_container_tar_path}/

mkdir -p %{buildroot}/%{_roles_path}
rsync -av ansible/roles/* %{buildroot}/%{_roles_path}/

install -D ansible/playbooks/kubernetes_storage.yaml %{buildroot}/%{_playbooks_path}/kubernetes_storage.yaml

%files
%{_caas_container_tar_path}/%{COMPONENT}:%{IMAGE_TAG}.tar
%{_roles_path}/kubernetes_storage
%{_playbooks_path}/kubernetes_storage.yaml

%preun

%post
mkdir -p %{_postconfig_path}
ln -s %{_playbooks_path}/kubernetes_storage.yaml %{_postconfig_path}/

%postun
if [ $1 -eq 0 ]; then
  rm -f %{_postconfig_path}/kubernetes_storage.yaml
fi

%clean
rm -rf ${buildroot}

