/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "dev-0yekb24q.us", // the auth0 domain prefix
    audience: "https://127.0.0.1:8100/tabs/user-page", // the audience set for the auth0 app
    clientId: "RLgaWcG7Ja5BWKTvR6b8KbPXDQvpAOo7", // the client id generated for the auth0 app
    callbackURL: "http://localhost:8100", // the base url of the running ionic application.
  },
};
