kubectl delete deploy flask-app-deployment-prod -n prod
kubectl delete deploy flask-app-deployment-stage -n staging
kubectl delete svc flask-app-service -n prod
kubectl delete svc flask-app-service -n staging
kubectl delete secret my-api-key-secret -n prod
kubectl delete secret my-api-key-secret -n staging
