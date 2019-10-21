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

FROM alpine:3.9

ARG go_install_dir="/usr/local/go"
ARG go_version
ARG DYNAMIC_LOCAL_PV_PROVISIONER_VERSION
ARG DEPENDENCY_MANAGER_VERSION
ENV GOPATH /build
ENV PATH $go_install_dir/bin:$PATH
ENV BUILD_DIR="$GOPATH/src/github.com/nokia/dynamic-local-pv-provisioner"

RUN apk update \
&&  apk upgrade \
&&  apk add --no-cache --virtual .build-deps build-base git mercurial go glide bash tar \
&&  apk add --no-cache curl e2fsprogs xfsprogs-extra \
&&  mkdir -p $go_install_dir \
&&  curl -fsSL -k https://dl.google.com/go/go${go_version}.src.tar.gz | tar zx --strip-components=1 -C ${go_install_dir} \
&&  cd ${go_install_dir}/src/ \
&&  ./make.bash \
&&  if [ $(uname -m) == 'aarch64' ]; then HOST_ARCH=arm64; else HOST_ARCH=amd64; fi \
&&  curl -fsSL -o /usr/local/bin/dep https://github.com/golang/dep/releases/download/v${DEPENDENCY_MANAGER_VERSION}/dep-linux-${HOST_ARCH} \
&&  chmod +x /usr/local/bin/dep \
&&  mkdir -p $BUILD_DIR \
&&  https://github.com/balintTobik/dynamic-local-pv-provisioner.git $BUILD_DIR \
# &&  git clone https://github.com/nokia/dynamic-local-pv-provisioner.git $BUILD_DIR \
&&  cd $BUILD_DIR \
&&  git fetch --tags \
&&  git checkout ${DYNAMIC_LOCAL_PV_PROVISIONER_VERSION} \
&&  dep init \
&&  dep ensure --vendor-only \
&&  CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o executor ./cmd/executor \
&&  mv $BUILD_DIR/executor /executor \
&&  CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o provisioner ./cmd/provisioner \
&&  mv $BUILD_DIR/provisioner /provisioner \
&&  apk del .build-deps \
&&  rm -rf $GOPATH \
&&  rm -rf $go_install_dir \
&&  rm -rf /build \
&&  rm -rf /root/.glide

