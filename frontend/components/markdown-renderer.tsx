"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <div className="markdown-content space-y-4 text-sm">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          a: ({ children, ...props }) => (
            <a {...props} className="text-cyan-300 underline decoration-cyan-300/40 underline-offset-4 transition-colors hover:text-cyan-200">
              {children}
            </a>
          ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-cyan-300/50 pl-4 text-slate-300">{children}</blockquote>
          ),
          ul: ({ children }) => <ul className="list-disc space-y-2 pl-5">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal space-y-2 pl-5">{children}</ol>,
          p: ({ children }) => <p className="leading-8 text-slate-300">{children}</p>,
          h1: ({ children }) => <h1 className="text-2xl font-semibold text-white">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold text-white">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-semibold text-white">{children}</h3>,
          pre: ({ children }) => <pre className="overflow-x-auto rounded-2xl border border-white/10 bg-slate-950/90 p-4">{children}</pre>,
          table: ({ children }) => (
            <div className="overflow-hidden rounded-2xl border border-white/10">
              <table className="w-full">{children}</table>
            </div>
          ),
          thead: ({ children }) => <thead>{children}</thead>,
          tbody: ({ children }) => <tbody>{children}</tbody>,
          tr: ({ children }) => <tr>{children}</tr>,
          th: ({ children }) => <th className="bg-white/6 px-3 py-2 text-left font-medium text-white">{children}</th>,
          td: ({ children }) => <td className="border-t border-white/10 px-3 py-2 align-top">{children}</td>,
          code: ({ children, ...props }) => (
            <code {...props} className="rounded-md bg-white/8 px-1.5 py-0.5 text-xs text-cyan-100">
              {children}
            </code>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
