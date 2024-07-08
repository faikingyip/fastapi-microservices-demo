import RollDown from "../ui/RollDown";
import classes from "./RootError.module.css";

export default function RootError({ errorMessage }) {
  return (
    <RollDown active={errorMessage}>
      {errorMessage && (
        <div className={`${classes["error-block"]}`}>
          <p className={`${classes["error-block-message"]}`}>{errorMessage}</p>
        </div>
      )}
    </RollDown>
  );
}
