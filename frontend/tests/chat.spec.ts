import { test, expect } from "@playwright/test";
const user = { id: 2, name: "Bruno Díaz", email: "bruno@example.test", role: "viewer", createdAt: "2025-06-10T15:30:00Z" };
test("consulta, sugerencias, lista vacía y recuperación de errores", async ({ page }) => {
  let attempt = 0;
  await page.route("**/api/chat", async route => {
    expect(route.request().postDataJSON().message).toBeTruthy();
    const replies = [{ result: [user], message: "Usuario encontrado", error: null }, { result: [], error: null }, { error: "Intención no reconocida.", examples: ["usuario 2"] }, { detail: [{ msg: "invalid" }] }, { result: [user] }];
    const current = attempt++;
    await route.fulfill({ status: current === 3 ? 422 : 200, json: replies[current] });
  });
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Enviar", exact: true })).toBeDisabled();
  await page.getByRole("button", { name: "usuario 2", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Bruno Díaz" })).toBeVisible();
  await expect(page.getByText("Usuario encontrado", { exact: true })).toBeVisible();
  await page.getByLabel("Tu consulta").fill("buscar nadie");
  await page.getByRole("button", { name: "Enviar", exact: true }).click();
  await expect(page.getByText("No se encontraron usuarios.")).toBeVisible();
  await page.getByLabel("Tu consulta").fill("hola");
  await page.getByRole("button", { name: "Enviar", exact: true }).click();
  await expect(page.getByText("Intención no reconocida.")).toBeVisible();
  await page.getByLabel("Tu consulta").fill("inválido");
  await page.getByLabel("Tu consulta").press("Enter");
  await expect(page.getByText("No pudimos procesar tu consulta.")).toBeVisible();
  await page.getByRole("button", { name: "lista 3", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Bruno Díaz" })).toHaveCount(2);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
test("integración real con Next, Orchestrator y Agent", async ({ page, request }) => {
  test.skip(!process.env.INTEGRATION, "Requiere ambos servicios FastAPI en ejecución");
  const invalid = await request.post("/api/chat", { data: { message: " " } });
  expect(invalid.status()).toBe(400);
  await page.goto("/");
  await page.screenshot({ path: `test-results/nexo-home-${test.info().project.name}.png`, fullPage: true, animations: "disabled" });
  await page.getByRole("button", { name: "usuario 2", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Bruno Díaz" })).toBeVisible();
  await page.screenshot({ path: `test-results/nexo-detail-${test.info().project.name}.png`, fullPage: true, animations: "disabled" });
  await page.getByRole("button", { name: "buscar ana", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Ana López" })).toBeVisible();
  await page.getByRole("button", { name: "lista 3", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Carla Ríos" })).toBeVisible();
  await page.getByRole("textbox", { name: "Tu consulta" }).fill("lista 10");
  await page.getByRole("textbox", { name: "Tu consulta" }).press("Enter");
  const latestReply = page.getByRole("log", { name: "Conversación" }).locator("article").last();
  await expect(latestReply.getByText("Pediste 10 usuarios, pero por ahora solo hay 5 disponibles. Probá con «lista 5».")).toBeVisible();
  await expect(latestReply).toHaveClass(/message-error/);
  await expect(latestReply.getByRole("heading")).toHaveCount(0);
  await page.screenshot({ path: `test-results/chat-${test.info().project.name}.png`, fullPage: true });
});

test("espera el arranque sin duplicar la consulta", async ({ page }) => {
  let attempts = 0;
  await page.route("**/api/chat", async route => {
    attempts++;
    await route.fulfill(attempts === 1 ? { status: 503, json: { code: "SERVICE_WARMING_UP" } } : { json: { result: [user] } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "usuario 2", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("está iniciándose");
  await expect(page.getByRole("button", { name: "lista 3", exact: true })).toBeDisabled();
  await expect(page.getByRole("heading", { name: "Bruno Díaz" })).toBeVisible();
  expect(attempts).toBe(2);
  await expect(page.getByText("usuario 2", { exact: true })).toHaveCount(2);
});
test("los errores permanentes no se reintentan", async ({ page }) => {
  let attempts = 0;
  await page.route("**/api/chat", async route => {
    attempts++;
    await route.fulfill({ status: 503, json: { error: "El servicio de chat todavía no está configurado." } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "usuario 2", exact: true }).click();
  await expect(page.getByText("El servicio de chat todavía no está configurado.")).toBeVisible();
  expect(attempts).toBe(1);
  await expect(page.getByRole("button", { name: "lista 3", exact: true })).toBeEnabled();
});
