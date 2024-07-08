import { Link } from "react-router-dom";
import FormLogin from "../components/FormLogin";
import classes from "./PageLogin.module.css";
export default function PageLogin() {
  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>Login</h2>
        <p className={`section-pitch-text`}>
          Log in to find your job or post a vacancy.
        </p>

        <FormLogin />
      </section>
      <section className={`section`}>
        <hr />
        <ul className={`related-links`}>
          <li>
            <Link to="/register">I don't have an account yet &gt;&gt;</Link>
          </li>
        </ul>
      </section>
    </>
  );
}
