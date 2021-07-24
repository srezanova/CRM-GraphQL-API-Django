import { createUseStyles } from 'react-jss';
import { theming } from '@mantine/core';

export default createUseStyles((theme) => ({
  wrapper: {
    minHeight: '100vh',
    backgroundColor: theme.colors.gray[0],
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },

  field: {
    marginBottom: theme.spacing.md,
  },

  inner: {
    width: 500,
  },

  title: {
    marginBottom: theme.spacing.xl * 1.5,
  },
}), { theming });
