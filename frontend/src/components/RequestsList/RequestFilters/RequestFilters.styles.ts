import { createUseStyles } from 'react-jss';
import { theming } from '@mantine/core';

export default createUseStyles((theme) => ({
  wrapper: {
    display: 'flex',
    margin: -5,
    marginBottom: theme.spacing.xl,
  },

  field: {
    flex: 1,
    margin: 5,
  },
}), { theming });
