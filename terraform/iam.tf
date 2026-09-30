resource "aws_iam_role" "app_ssm" {
  name = "${var.project_name}-app-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "app_ssm" {
  role       = aws_iam_role.app_ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "app_ssm" {
  name = "${var.project_name}-app-ssm-profile"
  role = aws_iam_role.app_ssm.name

  tags = {
    Project = var.project_name
  }
}
