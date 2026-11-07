import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Nexo | Directorio de usuarios", description: "Encontrá a quien buscás. Consultá el directorio de usuarios con una conversación." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body>{children}</body></html>;
}
