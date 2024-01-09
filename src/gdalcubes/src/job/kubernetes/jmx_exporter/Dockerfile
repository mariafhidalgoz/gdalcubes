FROM alpine/curl:3.14
WORKDIR /app/
# Copy the previously created config file to the mirror
COPY prometheus-jmx-config.yaml ./
# Download jmx prometheus javaagent jar online
RUN set -ex; \
     curl -L -O https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.17.2/jmx_prometheus_javaagent-0.17.2.jar;
