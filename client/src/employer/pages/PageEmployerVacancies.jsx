import { useQuery } from "@tanstack/react-query";
import classes from "./PageEmployerVacancies.module.css";
import LiVacancy from "../list-item/LiVacancy";
import { queryEmployerVacancies } from "../../tanstackqfns/query-employer-vacancies";
import { Link } from "react-router-dom";

export default function PageEmployerVacancies() {
  const queryEmployerVacs = useQuery({
    queryKey: ["employer-vacancies"],
    queryFn: queryEmployerVacancies,
    staleTime: 1000 * 60 * 5,
  });

  let content;
  if (queryEmployerVacs.isLoading) {
    content = <div>Loading...</div>;
  }

  if (queryEmployerVacs.isError) {
    throw queryEmployerVacs.error;
  }

  if (queryEmployerVacs.data) {
    content = (
      <ul>
        {queryEmployerVacs.data.data.results.map((vac, index) => (
          <li className={`list-item`} key={vac.id}>
            <LiVacancy
              id={vac.id}
              title={vac.title}
              daysInOffice={vac.days_in_office}
              workAddress={vac.work_address}
              workCity={vac.work_city}
              candidatesNeeded={vac.candidates_needed}
              isHiring={vac.is_hiring}
              createdOn={vac.created_on}
            />
            {index < queryEmployerVacs.data.data.results.length - 1 && <hr />}
          </li>
        ))}
      </ul>
    );
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Manage your vacancies
        </h2>
        {/* <p className={`section-text`}>
          Build your employer profile so you can tell us about a vacancy.
        </p> */}

        <div className={`section-body`}>{content}</div>
      </section>
      <section className={`section section-divider`}>
        <ul className={`related-links`}>
          <li>
            <Link to="/submit-vacancy">Submit a vacancy &gt;&gt;</Link>
          </li>
          <li>
            <Link to="/employer/vacancies">Manage your vacancies &gt;&gt;</Link>
          </li>
        </ul>
      </section>
    </>
  );
}
