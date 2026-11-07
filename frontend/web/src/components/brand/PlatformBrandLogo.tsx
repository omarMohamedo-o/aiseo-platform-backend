import React from "react";

interface PlatformBrandLogoProps {
  size?: number;
  showText?: boolean;
  className?: string;
  textClassName?: string;
  brandText?: string;
  onClick?: () => void;
}

export const PlatformBrandLogo: React.FC<PlatformBrandLogoProps> = ({
  size = 28,
  showText = true,
  className = "",
  textClassName = "text-xl font-bold tracking-tight text-slate-900",
  brandText = "esooai",
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onClick();
              }
            }
          : undefined
      }
      className={`flex items-center gap-2.5 ${
        onClick
          ? "cursor-pointer hover:opacity-85 transition-opacity select-none"
          : ""
      } ${className}`}
    >
      {/* Circular solid badge with 4-pointed white sparkle star */}
      <svg
        width={size}
        height={size}
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="shrink-0"
      >
        <circle cx="16" cy="16" r="16" fill="#0b0f19" />
        <path
          d="M 16 6 Q 16 16 6 16 Q 16 16 16 26 Q 16 16 26 16 Q 16 16 16 6 Z"
          fill="#ffffff"
        />
      </svg>
      {showText && <span className={textClassName}>{brandText}</span>}
    </div>
  );
};
