.PHONY: test test-cov deploy run-remote restart-service install-service

include .env
export

SSH_CMD = sshpass -p $(PI_PASSWORD) ssh -o StrictHostKeyChecking=no $(PI_USER)@$(PI_HOST)

test:
	.venv/bin/python -m pytest

test-cov:
	.venv/bin/python -m pytest --cov=piness --cov-report=term-missing --cov-report=html

deploy:
	@bash scripts/deploy.sh

run-remote:
	$(SSH_CMD) "cd $(PI_DEPLOY_PATH) && venv/bin/python -m piness.main"

restart-service:
	$(SSH_CMD) "sudo systemctl restart piness"

install-service:
	sshpass -p $(PI_PASSWORD) scp -o StrictHostKeyChecking=no scripts/piness.service $(PI_USER)@$(PI_HOST):/tmp/piness.service
	$(SSH_CMD) "sudo mv /tmp/piness.service /etc/systemd/system/piness.service && sudo systemctl daemon-reload && sudo systemctl enable piness"
