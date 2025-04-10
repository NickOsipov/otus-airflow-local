variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "localhost"
}

group "default" {
  targets = ["airflow-local"]
}

target "airflow-local" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["airflow-local:${TAG}"]
}