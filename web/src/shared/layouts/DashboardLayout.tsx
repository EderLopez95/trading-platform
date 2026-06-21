import { type ReactNode } from "react";
import Navbar from "@/shared/components/Navbar";

type Props = {
  children: ReactNode;
};

export default function DashboardLayout({
  children,
}: Props) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  );
}
