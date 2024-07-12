import classes from "./LiVacancy.module.css";
import { Link } from "react-router-dom";
import { formatDate } from "../../utils/utils-formatter";

export default function LiVacancy({
  id,
  title,
  createdOn,
  isHiring,
  candidatesNeeded,
  daysInOffice,
  workAddress,
  workCity,
}) {

  return (
    <div className="list-item-content">
      <div>
        <Link to={`/employer/vacancies/${id}`} className={`${classes["list-item-title"]}`}>{title}</Link>
      </div>
      <div>
        <span className={`${classes["field-label"]}`}>Days in office:</span>
        <span className={`${classes["field-value"]}`}>{daysInOffice}</span>
        {daysInOffice === 0 ? (
          <span className={`${classes["field-value"]}`}>(Fully remote)</span>
        ) : undefined}
      </div>
      <div>
        <span className={`${classes["field-label"]}`}>Location:</span>
        {workAddress && (
          <span className={`${classes["field-value"]}`}>{workAddress}</span>
        )}
        {workCity && (
          <span className={`${classes["field-value"]}`}>({workCity})</span>
        )}
      </div>
      <div>
        <span className={`${classes["field-label"]}`}>Candidates needed:</span>
        <span className={`${classes["field-value"]}`}>{candidatesNeeded}</span>
      </div>
      <div>
        <span className={`${classes["field-label"]}`}>Is hiring:</span>
        <span className={`${classes["field-value"]}`}>
          {isHiring ? "Yes" : "No"}
        </span>
      </div>
      <div>
        <span className={`${classes["field-label"]}`}>Created on:</span>
        <span className={`${classes["field-value"]}`}>
          {formatDate(new Date(createdOn))}
        </span>
      </div>
    </div>
  );
}
