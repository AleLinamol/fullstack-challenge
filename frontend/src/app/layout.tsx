import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Jahi | Chat de usuarios", description: "Explora usuarios mediante un chat conectado a servicios FastAPI." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body>{children}</body></html>;
}
