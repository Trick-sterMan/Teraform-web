variable "aws_region" {
  description = "AWS Region deploy he thong"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Ten du an ecommerce"
  type        = string
  default     = "ecommerce"
}

variable "instance_type" {
  description = "Loai EC2 instance cho cac backend servers"
  type        = string
  default     = "t2.micro"
}
