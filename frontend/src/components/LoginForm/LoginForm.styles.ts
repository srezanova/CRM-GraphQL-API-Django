import { createUseStyles } from 'react-jss';
import { theming } from '@mantine/core';

export default createUseStyles((theme) => ({
  wrapper: {
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.colors.gray[0],
  },

  title: {
    marginBottom: theme.spacing.xl * 1.5,
  },

  field: {
    marginBottom: theme.spacing.md,
  },

  inner: {
    width: 400,
  },

  controls: {
    marginTop: theme.spacing.lg,
  },
}), { theming });
