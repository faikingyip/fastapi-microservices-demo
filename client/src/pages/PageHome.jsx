import { Link, NavLink } from "react-router-dom";
import classes from "./PageHome.module.css";

export default function PageHome() {
  return (
    <>
      <section className={`section ${classes["section-about-us"]}`}>
        <h2 className={`section-title section-title-color-red`}>About us</h2>
        <p className={`section-pitch-text`}>Welcome to Fai's demo app!</p>
        <p className={`section-text`}>
          This is a simplified banking application that allow users to deposit
          and withdraw funds. While simple in features, this application is
          built using various technologies, including microservices developed
          using FastAPI and a RabbitMQ messaging bus to allow these
          microservices to communicate.
        </p>
        <p className={`section-text`}>Enjoy!</p>
      </section>

      <section className={`section ${classes["section-microservices-demo"]}`}>
        <h2 className={`section-title section-title-color-wood`}>
          Microservices demo app
        </h2>
        <ul className={`${classes["links"]}`}>
          <li className={`${classes["section-link-item"]}`}>
            <NavLink to="/microservices-demo">Give it a go. &gt;&gt;</NavLink>
          </li>
        </ul>
      </section>
    </>
    // <>
    //   <section className={`section ${classes["section-about-us"]}`}>
    //     <h2 className={`section-title section-title-color-red`}>About us</h2>
    //     <p className={`section-pitch-text`}>
    //       Welcome to the Codelocks zone of recruiting!
    //     </p>
    //     <p className={`section-text`}>
    //       At Codelocks Recruitment, we bridge the gap between employers seeking
    //       talent and jobseekers pursuing their next career opportunity. We
    //       handle the heavy lifting behind the scenes to provide seamless
    //       connections, ensuring a win-win situation for everyone involved.
    //     </p>
    //   </section>

    //   <section className={`section ${classes["section-employers"]}`}>
    //     <h2 className={`section-title section-title-color-wood`}>Employers</h2>
    //     <ul className={`${classes["links"]}`}>
    //       <li className={`${classes["section-link-item"]}`}>
    //         <NavLink to="/submit-vacancy">
    //           Tell us about a vacancy &gt;&gt;
    //         </NavLink>
    //       </li>
    //       {/* <li>
    //         <NavLink to="#">Search our active jobseekers &gt;&gt;</NavLink>
    //       </li> */}
    //       {/* <li>
    //         <NavLink to="#">Get notified of new jobseekers &gt;&gt;</NavLink>
    //       </li> */}
    //     </ul>
    //   </section>

    //   <section className={`section ${classes["section-jobseekers"]}`}>
    //     <h2 className={`section-title section-title-color-wood`}>Jobseekers</h2>
    //     <ul className={`${classes["links"]}`}>
    //       <li className={`${classes["section-link-item"]}`}>
    //         <NavLink to="/build-my-job-search-profile">
    //           Publish your jobseeking profile &gt;&gt;
    //         </NavLink>
    //       </li>
    //       <li className={`${classes["section-link-item"]}`}>
    //         <NavLink to="/search-jobs">Search jobs &gt;&gt;</NavLink>
    //       </li>
    //       <li className={`${classes["section-link-item"]}`}>
    //         <NavLink to="/set-job-alerts">Set up job alerts &gt;&gt;</NavLink>
    //       </li>
    //     </ul>
    //   </section>
    // </>
  );
}
