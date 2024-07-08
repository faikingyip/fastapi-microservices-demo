import { forwardRef, useState } from "react";
import RollDown from "../ui/RollDown";
import classes from "./InputGroup.module.css";

const InputGroup = forwardRef(function InputGroup(
  { id, label, errorMessage, ...props },
  ref
) {
  const [currentErrorMessage, setCurrentErrorMessage] = useState(errorMessage);

  /**
   * Clears the current message only after the roll up is completed.
   * This is required for a smooth transition.
   */
  function handleOnRollUpCompleted() {
    setCurrentErrorMessage("");
  }

  /**
   * Roll down starts when the errorMessage prop changes.
   * Once roll down is completed, we store the value of errorMessage
   * into currentErrorMessage. This is because errorMessage can be set to
   * empty, causing a not smooth transition. In order for a smooth transition,
   * we need to keep the message in the error box until after roll up is
   * completed. By storing a copy of the message, we guarentee the message
   * is displayed in the box until roll up is completed.
   */
  function handleOnRollDownCompleted() {
    if (errorMessage && errorMessage != currentErrorMessage) {
      setCurrentErrorMessage(errorMessage);
    }
  }

  /**
   * We run an addition check whenever the component function is rerun,
   * so that if the message from prop is different from that of the currently buffered
   * message, then we sync it up. We also want to ignore this if the new errorMessage
   * is empty. This ensures if there are different messages that can be displayed,
   * they won't flip from one to another unpredictably.
   */
  if (errorMessage && errorMessage != currentErrorMessage) {
    setCurrentErrorMessage(errorMessage);
  }

  return (
    <div className={`${classes["input-group"]}`}>
      <label className={`${classes["input-label"]}`} htmlFor={id}>
        {label}
      </label>
      <input
        ref={ref}
        className={`${classes["input-control"]}`}
        id={id}
        {...props}
      />
      <RollDown
        active={errorMessage}
        onRollUpCompleted={handleOnRollUpCompleted}
        onRollDownCompleted={handleOnRollDownCompleted}
      >
        <div className={`${classes["input-validation-message-block"]}`}>
          <p>{errorMessage || currentErrorMessage}</p>
        </div>
      </RollDown>
    </div>
  );
});

export default InputGroup;
