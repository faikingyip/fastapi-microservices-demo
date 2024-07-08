import { useState } from "react";
import classes from "./RollDown.module.css";

export default function RollDown({
  children,
  active,
  maxHeight,
  onRollUpCompleted,
  onRollDownCompleted,
}) {
  const [isRolledUp, setIsRolledUp] = useState(true);

  const handleTransitionEnd = (e) => {
    const newRollUpState = !isRolledUp;

    if (newRollUpState) {
      if (onRollUpCompleted) {
        onRollUpCompleted();
      }
    } else {
      if (onRollDownCompleted) {
        onRollDownCompleted();
      }
    }

    setIsRolledUp((prev) => {
      return !prev;
    });
  };

  const contentStyle = {
    maxHeight: maxHeight || "20rem",
    // transition: "max-height 0.5s ease-out",
  };

  return (
    <div
      style={active ? contentStyle : undefined}
      className={`${classes.block}`}
      onTransitionEnd={handleTransitionEnd}
    >
      {children}
    </div>
  );
}
