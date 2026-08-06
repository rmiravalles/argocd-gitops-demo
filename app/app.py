from os import getenv

from flask import Flask, jsonify, render_template


def _split_list(value: str) -> list[str]:
	return [item.strip() for item in value.split(",") if item.strip()]


def load_demo_context() -> dict[str, object]:
	return {
		"app_name": getenv("APP_NAME", "GitOps Demo"),
		"app_version": getenv("APP_VERSION", "v1.0.0"),
		"commit_sha": getenv("COMMIT_SHA", "local-dev"),
		"environment": getenv("APP_ENVIRONMENT", "development"),
		"deployment_message": getenv(
			"DEPLOYMENT_MESSAGE",
			"ArgoCD continuously reconciles the running environment with the Git repository, enabling version-controlled, auditable, and declarative deployments.",
		),
		"accent_color": getenv("ACCENT_COLOR", "#0f766e"),
		"cluster_name": getenv("CLUSTER_NAME", "demo-cluster"),
		"namespace": getenv("APP_NAMESPACE", "app-gitops-demo"),
		"image": getenv("APP_IMAGE", "ghcr.io/rmiravalles/argocd-gitops-demo:latest"),
		"sync_status": getenv("ARGOCD_SYNC_STATUS", "Synced"),
		"health_status": getenv("ARGOCD_HEALTH_STATUS", "Healthy"),
		"features": _split_list(
			getenv(
				"APP_FEATURES",
				"manifest-driven release, repeatable syncs, visible rollout changes, Git as source of truth",
			)
		),
	}


app = Flask(__name__)


@app.route("/")
def index() -> str:
	return render_template("index.html", demo=load_demo_context())


@app.route("/api/context")
def api_context():
	return jsonify(load_demo_context())


@app.route("/healthz")
def healthz():
	return {"status": "ok"}


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(getenv("PORT", "8081")), debug=False)
