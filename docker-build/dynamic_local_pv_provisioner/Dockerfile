FROM alpine:3.9

ARG go_install_dir="/usr/local/go"
ARG go_version
ARG DYNAMIC_LOCAL_PV_PROVISIONER_VERSION
ARG DEPENDENCY_MANAGER_VERSION
ENV FIXED_HASH_DYNAMIC_LOCAL_PV_PROVISIONER_VERSION 1640cb0515eed0762156f7ef0c82d722c8ec5352
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
&&  curl -fsSL -o /usr/local/bin/dep https://github.com/golang/dep/releases/download/v${DEPENDENCY_MANAGER_VERSION}/dep-linux-amd64 \
&&  chmod +x /usr/local/bin/dep \
&&  mkdir -p $BUILD_DIR \
&&  git clone https://github.com/balintTobik/dynamic-local-pv-provisioner.git $BUILD_DIR \
&&  cd $BUILD_DIR \
&&  git fetch --tags \
&&  git checkout ${FIXED_HASH_DYNAMIC_LOCAL_PV_PROVISIONER_VERSION} \
&&  dep init \
&&  dep ensure --vendor-only \
&&  CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o executor ./cmd/executor \
&&  mv $BUILD_DIR/executor /executor \
&&  apk del .build-deps \
&&  rm -rf $GOPATH \
&&  rm -rf $go_install_dir \
&&  rm -rf /build \
&&  rm -rf /root/.glide

