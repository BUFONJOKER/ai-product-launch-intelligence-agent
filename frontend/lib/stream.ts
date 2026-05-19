import { StreamEvent } from "@/lib/types";

export async function readStreamEvents(
  response: Response,
  onEvent: (event: StreamEvent) => void,
) {
  const reader = response.body?.getReader();

  if (!reader) {
    return;
  }

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });

    let splitIndex = buffer.indexOf("\n\n");

    while (splitIndex !== -1) {
      const chunk = buffer.slice(0, splitIndex).trim();
      buffer = buffer.slice(splitIndex + 2);
      splitIndex = buffer.indexOf("\n\n");

      if (!chunk) {
        continue;
      }

      const jsonText = chunk
        .split("\n")
        .map((line) => line.replace(/^data:\s?/, ""))
        .join("\n")
        .trim();

      if (!jsonText) {
        continue;
      }

      try {
        onEvent(JSON.parse(jsonText) as StreamEvent);
      } catch {
        // Ignore malformed chunks and continue reading.
      }
    }
  }
}
