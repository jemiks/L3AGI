import React from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';

const AiMessageMarkdown = ({ children }: { children: any }) => {
  return (
    <StyledReactMarkdown
      children={children}
      remarkPlugins={[[remarkGfm, { singleTilde: false }]]}
      components={{
        table: ({ node, ...props }) => <StyledTable {...props} />,
        a: ({ href, children }) => {
          const youtubeRegex = /^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)&/;

          if (youtubeRegex.test(href as string)) {
            const videoId = (href as string).match(youtubeRegex)?.[1];
            return (
              <iframe
                width="560"
                height="315"
                src={`https://www.youtube.com/embed/${videoId}`}
                title="YouTube video player"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            );
          }

          return <a href={href as string}>{children}</a>;
        },
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || 'language-js');
          return !inline && match ? (
            <SyntaxHighlighter
              children={String(children).replace(/\n$/, '')}
              style={atomDark as any}
              language={match[1]}
              PreTag='div'
              {...props}
            />
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        },
      }}
    />
  );
};

export default AiMessageMarkdown;

const StyledReactMarkdown = styled(ReactMarkdown)`
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const StyledTable = styled.table`
  border-collapse: collapse;

  th,
  td {
    border: 1px solid #fff;
    padding: 5px 30px;
    text-align: center;
  }
`;
