# fastapi-microservices-demo


kubectl get pods
kubectl exec -it auth-depl-69589f7cfd-djrtl -- sh

minikube service auth-srv


## Tools
- Scaffold
- Kubernetes
- Minikube
- ingress nginx
- alembic


##### Error handling throughout all services.
- Errors are categorized into Validation errors and Application errors.

- Application errors are represented by the AppServiceError object and are errors
where the details should not be sent back to the client, i.e. database errors
Instead, these errors are handled behind the scenes, i.e. logged, and a
generic system error message will be returned to the client.

- Validation errors can be categorized further into data validation errors
and business logic validation errors.

- Data validation errors, i.e. email format, lengths, min values, etc, are
defined in the pydantic schemas and will have automatic validation. If there
are validation errors, these they will be represented by the
HTTPValidationError object.

- Business logic validation errors are custom logic errors, such as email
address already in use when the user tries to sign up. These errors are
represented by the BusinessValidationError object.

- While HTTPValidationError performed by pydantic will automatically be
sent back to the client as a response, BusinessValidationError and app error
need to be processed and shaped into a consistent format before sending back
to the client. This approach will allow the client to process errors
consistently.

