import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import InfoIcon from '@mui/icons-material/Info';
import { Box, Card, CardContent, Grid, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import React from 'react';
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts';

const OEEDashboard = ({ oeeData, deviceId, location, month }) => {
  // Format data for charts
  const formatChartData = (data) => {
    if (!data || !data.oee) return [];
    return [
      {
        name: 'Current',
        OEE: data.oee,
        Availability: data.availability,
        Performance: data.performance,
        Quality: data.quality,
      }
    ];
  };

  const chartData = formatChartData(oeeData);

  // Calculate trends and insights
  const getTrends = () => {
    if (!oeeData) return [];
    const trends = [];
    
    if (oeeData.oee < 85) {
      trends.push({
        type: 'warning',
        message: 'OEE is below industry standard (85%)'
      });
    }
    
    if (oeeData.availability < 90) {
      trends.push({
        type: 'improvement',
        message: 'Availability can be improved through better maintenance scheduling'
      });
    }
    
    if (oeeData.quality < 95) {
      trends.push({
        type: 'action',
        message: 'Quality issues detected - Check production parameters'
      });
    }
    
    return trends;
  };

  const getIconByType = (type) => {
    switch (type) {
      case 'warning':
        return <ErrorIcon color="error" />;
      case 'improvement':
        return <InfoIcon color="primary" />;
      default:
        return <CheckCircleIcon color="success" />;
    }
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        {/* OEE Overview Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                OEE Overview
              </Typography>
              <LineChart width={500} height={300} data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="OEE" stroke="#8884d8" />
                <Line type="monotone" dataKey="Availability" stroke="#82ca9d" />
                <Line type="monotone" dataKey="Performance" stroke="#ffc658" />
                <Line type="monotone" dataKey="Quality" stroke="#ff7300" />
              </LineChart>
            </CardContent>
          </Card>
        </Grid>

        {/* Insights and Recommendations */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Insights & Recommendations
              </Typography>
              <List>
                {getTrends().map((trend, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      {getIconByType(trend.type)}
                    </ListItemIcon>
                    <ListItemText primary={trend.message} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* KPI Cards */}
        <Grid item xs={12}>
          <Grid container spacing={2}>
            <Grid item xs={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    OEE
                  </Typography>
                  <Typography variant="h4">
                    {oeeData?.oee || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Availability
                  </Typography>
                  <Typography variant="h4">
                    {oeeData?.availability || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Performance
                  </Typography>
                  <Typography variant="h4">
                    {oeeData?.performance || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Quality
                  </Typography>
                  <Typography variant="h4">
                    {oeeData?.quality || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default OEEDashboard; 