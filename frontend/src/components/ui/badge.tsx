// PROVIDED. Do not modify.

import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type Variant = "default" | "secondary" | "outline" | "success" | "warning" | "destructive";

const VARIANTS: Record<Variant, string> = {
  default: "bg-primary text-primary-foreground",
  secondary: "bg-secondary text-secondary-foreground",
  outline: "border border-border text-foreground",
  success: "bg-success/15 text-success border border-success/30",
  warning: "bg-warning/15 text-warning border border-warning/30",
  destructive: "bg-destructive/15 text-destructive border border-destructive/30",
};

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: Variant;
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex w-fit shrink-0 items-center gap-1 rounded-full px-2 py-0.5",
        "text-xs font-medium whitespace-nowrap [&>svg]:size-3 [&>svg]:shrink-0",
        VARIANTS[variant],
        className,
      )}
      {...props}
    />
  );
}
