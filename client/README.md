# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


# TODO
## Comment
## Throw errors
## APIs into backend namespace
## Remove hardcoding
## Close knowledge form upon submission.


## Approach

### Forms
We use React Hook Forms and Zod to simplify the creation of forms. These libraries are well documented and there are plenty of examples online, which makes this approach easy to maintain.

### API calls and other places that store data
For handling get and mutation of data using API calls and other places that store data, we use Tanstack query, which provides comprehensive features such as caching and auto refresh of data. Reach Hook Forms also provide good support for submission of data to the backend, but using Tanstack allows us to standardise get and mutate operations beyond the context of forms.