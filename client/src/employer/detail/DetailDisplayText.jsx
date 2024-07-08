import { useState } from "react";
import Modal from "../../components/Modal";
import classes from "./DetailDisplayText.module.css";
import FormEditDetailText from "../forms/FormEditDetailText";


export default function DetailDisplayText({
  fieldName,
  fieldTitle,
  fieldValue,
  zodSchema,
  mutationFn,
  queriesToInvalidateOnSuccess
}) {
  const [isUpdating, setIsUpdating] = useState(false);

  function handleOnStartUpdate(e) {
    setIsUpdating(true);
  }

  function handleOnStopUpdate(e) {
    setIsUpdating(false);
  }

  function handleOnUpdateDetailSuccess(e) {
    setIsUpdating(false);
  }

  let displayValue;
  if (typeof fieldValue === 'boolean') {
    displayValue = fieldValue ? "Yes" : "No"
  } else {
    displayValue = fieldValue || fieldValue === 0 ? fieldValue : <>&lt;Not set&gt;</>
  }

  return (
    <>
      {isUpdating && (
        <Modal onClose={handleOnStopUpdate}>
          <div className={`form-container`}>
            <h2 className={`form-title form-title-color-standard`}>
              Update your detail
            </h2>
            <FormEditDetailText
              fieldName={fieldName}
              fieldTitle={fieldTitle}
              initialFieldValue={fieldValue}
              zodSchema={zodSchema}
              mutationFn={mutationFn}
              queriesToInvalidateOnSuccess={queriesToInvalidateOnSuccess}
              onCancelClick={handleOnStopUpdate}
              onSuccess={handleOnUpdateDetailSuccess}
            />
          </div>
        </Modal>
      )}
      <div className={`${classes["field-detail"]}`}>
        <div className={`${classes["field-heading"]}`}>
          <h3 className={`${classes["field-name"]}`}>{fieldTitle}</h3>
          <button
            type="button"
            onClick={handleOnStartUpdate}
            className={`button button-color-proceed ${classes["action-button"]}`}
          >
            Change
          </button>
        </div>

        <span className={`${classes["field-value"]}`}>
          {displayValue}
        </span>
      </div>
    </>
  );
}
