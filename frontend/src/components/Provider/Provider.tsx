import { MantineProvider, GlobalStyles, NormalizeCSS } from '@mantine/core';
import { ApolloProvider } from '@apollo/client';
import { apolloClient } from './apollo.client';

interface ProviderProps {
  children: React.ReactNode;
}

export function Provider({ children }: ProviderProps) {
  return (
    <ApolloProvider client={apolloClient}>
      <MantineProvider>
        <GlobalStyles />
        <NormalizeCSS />
        {children}
      </MantineProvider>
    </ApolloProvider>
  );
}
