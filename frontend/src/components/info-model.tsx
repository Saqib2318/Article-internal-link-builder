import React, { useEffect, useRef, useState } from "react";

const ToastMessage: React.FC<{ message: string; onClose: () => void }> = ({
  message,
  onClose,
}) => {
  const [visible, setVisible] = useState(true);
  const [progress, setProgress] = useState(0);
  const duration = 5000; // 5 seconds
  const intervalRef = useRef<any>(null);

  useEffect(() => {
    setVisible(true);
    setProgress(0);

    const start = Date.now();
    intervalRef.current = setInterval(() => {
      const elapsed = Date.now() - start;
      const percent = Math.min((elapsed / duration) * 100, 100);
      setProgress(percent);
      if (percent === 100) {
        setVisible(false);
        onClose();
      }
    }, 30);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [onClose]);

  if (!visible) return null;

  return (
    <div
      className={`
        fixed bottom-6 right-6 z-50
        transition-transform duration-300
        ${visible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"}
        max-w-xs w-full
      `}
    >
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded shadow-lg relative w-full h-12 flex gap-6 items-center">
        <div className=" w-full flex items-center justify-between px-6">
          <span className="mr-4">{message}</span>
          <button
            className="text-red-500 font-bold border flex justify-center items-center w-6 h-6 rounded-full hover:bg-red-100 transition"
            onClick={() => {
              setVisible(false);
              onClose();
            }}
            aria-label="Close"
          >
           <span> × </span>
          </button>
        </div>
        {/* Animated bottom border */}
        <div className="absolute left-0 bottom-0 h-1 w-full">
          <div
            className="h-full bg-gradient-to-r from-red-400 to-red-600 transition-all"
            style={{
              width: `${progress}%`,
              transition: "width 30ms linear",
            }}
          />
        </div>
      </div>
    </div>
  );
};
export default ToastMessage;