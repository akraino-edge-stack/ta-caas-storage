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
MAINTAINER Balazs Szekeres <balazs.szekeres@nokia.com>

ARG STORAGE_LOCAL_STATIC_PROVISIONER_VERSION
ARG go_install_dir="/usr/local/go"
ARG go_version

ENV PATH="$go_install_dir/bin:$PATH"
ENV GOPATH /build
ENV USER=root

RUN apk update \
&&  apk upgrade \
&&  apk add --no-cache --virtual .build-deps build-base go godep curl tar \
&&  apk add util-linux e2fsprogs bash xfsprogs \
\
&&  mkdir -p $go_install_dir \
&&  curl -fsSL -k https://dl.google.com/go/go${go_version}.src.tar.gz | tar zx --strip-components=1 -C ${go_install_dir} \
&&  cd ${go_install_dir}/src/ \
&&  ./make.bash \
\
&&  mkdir -p ${GOPATH}/src/sigs.k8s.io/sig-storage-local-static-provisioner \
&&  curl -fsSL -k https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/archive/v${STORAGE_LOCAL_STATIC_PROVISIONER_VERSION}.tar.gz | tar zx --strip-components=1 -C ${GOPATH}/src/sigs.k8s.io/sig-storage-local-static-provisioner \
&&  cd ${GOPATH}/src/sigs.k8s.io/sig-storage-local-static-provisioner \
&&  GOOS=${OS} GOARCH=${ARCH} go build -a -ldflags '-extldflags "-static"' -o _output/${OS}/${ARCH}/local-volume-provisioner ./cmd/local-volume-provisioner \
&&  mv deployment/docker/scripts /scripts \
&&  mv deployment/docker/test.sh /test.sh \
&&  mv _output/${OS}/${ARCH}/local-volume-provisioner /bin/local-volume-provisioner \
&&  apk del .build-deps \
&&  rm -rf /build \
&&  rm -rf ${GOPATH}

ENTRYPOINT ["/bin/local-volume-provisioner"]
