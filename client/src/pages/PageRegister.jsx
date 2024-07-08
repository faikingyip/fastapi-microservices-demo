import FormRegister from "../components/FormRegister";
import authActions from "../store-localstorage/auth-actions";

export default function PageRegister() {
  authActions.clearAuthTokens();
  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Register with us
        </h2>
        <p className={`section-pitch-text`}>
          Make your next career move a smooth one.
        </p>
        <FormRegister />
      </section>
    </>
  );
}
