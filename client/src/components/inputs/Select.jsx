import { forwardRef } from "react";

const Select = forwardRef(function Select(
  {
    options,
    blankSelectionText,
    valueFieldName = "value",
    textFieldName = "text",
    multiple,
    ...props
  },
  ref
) {
  if (multiple) {
    throw new Error(
      "Only the single value configuration is allowed for the Select component."
    );
  }

  return (
    <select {...props} ref={ref}>
      <option value="">
        {blankSelectionText ? blankSelectionText : "--- Choose ---"}
      </option>
      {options.map((option) => (
        <option key={option[valueFieldName]} value={option[valueFieldName]}>
          {option[textFieldName]}
        </option>
      ))}
    </select>
  );
});

export default Select;
