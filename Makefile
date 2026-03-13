.PHONY: test test-cov deploy run-remote restart-service install-service

test:
	python -m pytest

test-cov:
	python -m pytest --cov=piness --cov-report=term-missing --cov-report=html

deploy:
	@bash scripts/deploy.sh

run-remote:
	@set -a && . ./.env && set +a && \
	ssh $${PI_USER}@$${PI_HOST} "cd $${PI_DEPLOY_PATH} && python -m piness.main"

restart-service:
	@set -a && . ./.env && set +a && \
	ssh $${PI_USER}@$${PI_HOST} "sudo systemctl restart piness"

install-service:
	@set -a && . ./.env && set +a && \
	scp scripts/piness.service $${PI_USER}@$${PI_HOST}:/tmp/piness.service && \
	ssh $${PI_USER}@$${PI_HOST} "sudo mv /tmp/piness.service /etc/systemd/system/piness.service && sudo systemctl daemon-reload && sudo systemctl enable piness"
