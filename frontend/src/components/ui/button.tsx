import * as React from "react";
import { cn } from "@/lib/parser";

const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, ...props }, ref) => {
  return (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-950 disabled:pointer-events-none disabled:opacity-50",
        "bg-blue-600 hover:bg-blue-700 text-white px-4 py-2",
        className
      )}
      {...props}
    />
  );
});
Button.displayName = "Button";

export { Button };