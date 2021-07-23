import { createUseStyles } from 'react-jss';
import { theming } from '@mantine/core';

export default createUseStyles((theme) => ({
  wrapper: {
    backgroundColor: theme.colors.gray[0],
    minHeight: '100vh',
    paddingTop: theme.spacing.xl * 2,
    paddingBottom: theme.spacing.xl * 2,
  },

  header: {
    marginBottom: theme.spacing.md,
  },
}), { theming });
