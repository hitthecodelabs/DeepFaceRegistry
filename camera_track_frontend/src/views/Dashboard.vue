<template>
  <div>

    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <!-- Card stats -->
      <b-row>
        <b-col xl="4" md="6">
          <stats-card title="Total de Usuarios"
                      type="gradient-red"
                      :sub-title="''+total_users"
                      icon="ni ni-single-02"
                      class="mb-4">

          </stats-card>
        </b-col>
        <b-col xl="4" md="6">
          <stats-card title="Total de Cámaras"
                      type="gradient-orange"
                      :sub-title="''+total_cameras"
                      icon="ni ni-camera-compact"
                      class="mb-4">

          </stats-card>
        </b-col>
        <b-col xl="4" md="6">
          <stats-card title="Total de Grabaciones"
                      type="gradient-green"
                      :sub-title="''+total_clips"
                      icon="ni ni-folder-17"
                      class="mb-4">

          </stats-card>

        </b-col>
        <!--<b-col xl="3" md="6">
          <stats-card title="Performance"
                      type="gradient-info"
                      sub-title="49,65%"
                      icon="ni ni-chart-bar-32"
                      class="mb-4">

            <template slot="footer">
              <span class="text-success mr-2">54.8%</span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </b-col>-->
      </b-row>
    </base-header>

    <!--Charts-->
    <b-container fluid class="mt--7">
      <b-row>
        <!--<b-col xl="8" class="mb-5 mb-xl-0">
          <card type="default" header-classes="bg-transparent">
            <b-row align-v="center" slot="header">
              <b-col>
                <h6 class="text-light text-uppercase ls-1 mb-1">Overview</h6>
                <h5 class="h3 text-white mb-0">Sales value</h5>
              </b-col>
              <b-col>
                <b-nav class="nav-pills justify-content-end">
                  <b-nav-item
                       class="mr-2 mr-md-0"
                       :active="bigLineChart.activeIndex === 0"
                       link-classes="py-2 px-3"
                       @click.prevent="initBigChart(0)">
                      <span class="d-none d-md-block">Month</span>
                      <span class="d-md-none">M</span>
                  </b-nav-item>
                  <b-nav-item
                    link-classes="py-2 px-3"
                    :active="bigLineChart.activeIndex === 1"
                    @click.prevent="initBigChart(1)"
                  >
                    <span class="d-none d-md-block">Week</span>
                    <span class="d-md-none">W</span>
                  </b-nav-item>
                </b-nav>
              </b-col>
            </b-row>
            <line-chart
              :height="350"
              ref="bigChart"
              :chart-data="bigLineChart.chartData"
              :extra-options="bigLineChart.extraOptions"
            >
            </line-chart>
          </card>
        </b-col>-->

        <b-col xl="12" class="mb-5 mb-xl-0">
          <card header-classes="bg-transparent">
            <b-row align-v="center" slot="header">
              <b-col>
                <h6 class="text-uppercase text-muted ls-1 mb-1">Actualmente</h6>
                <h5 class="h3 mb-0">Total de grabaciones</h5>
              </b-col>
            </b-row>

            <bar-chart
              v-if="loaded"
              :height="350"
              ref="barChart"
              :chart-data="redBarChart.chartData"
            >
            </bar-chart>
          </card>
        </b-col>
      </b-row>
      <!-- End charts-->

      <!--Tables-->
      <b-row class="mt-5">
        <b-col xl="12" class="mb-5 mb-xl-0">
          <!--<page-visits-table></page-visits-table>-->
          <!--<last-change-users-table :data="last_change_users"></last-change-users-table>-->
          <last-change-users-table ></last-change-users-table>
        </b-col>
        <!--<b-col xl="4" class="mb-5 mb-xl-0">
          <social-traffic-table></social-traffic-table>
        </b-col>-->
      </b-row>
      <!--End tables-->
    </b-container>

  </div>
</template>
<script>
  // Charts
  import * as chartConfigs from '@/components/Charts/config';
  import LineChart from '@/components/Charts/LineChart';
  import BarChart from '@/components/Charts/BarChart';

  // Components
  import BaseProgress from '@/components/BaseProgress';
  import StatsCard from '@/components/Cards/StatsCard';

  // Tables
  import SocialTrafficTable from './Dashboard/SocialTrafficTable';
  import PageVisitsTable from './Dashboard/PageVisitsTable';
  import LastChangeUsersTable from './Dashboard/LastChangeUsersTable';

  export default {
    components: {
      LineChart,
      BarChart,
      BaseProgress,
      StatsCard,
      PageVisitsTable,
      SocialTrafficTable,
      LastChangeUsersTable
    },
    data() {
      return {
        bigLineChart: {
          allData: [
            [0, 20, 10, 30, 15, 40, 20, 60, 60],
            [0, 20, 5, 25, 10, 30, 15, 40, 40]
          ],
          activeIndex: 0,
          chartData: {
            datasets: [
              {
                label: 'Performance',
                data: [0, 20, 10, 30, 15, 40, 20, 60, 60],
              }
            ],
            labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          },
          extraOptions: chartConfigs.blueChartOptions,
        },
        redBarChart: {
          /*chartData: {
            labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'Sales',
              data: [25, 20, 30, 22, 17, 29]
            }]
          },*/
          chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'Grabaciones',
              data: [0, 20, 30, 22, 17, 29, 25, 20, 30, 22, 17, 29]
              //data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }]
          },
          extraOptions: chartConfigs.blueChartOptions
        },
        loaded: false,
        total_users : 0,
        total_cameras : 0,
        total_clips: 0,
        last_change_users : []
      };
    },
    methods: {
      initBigChart(index) {
        let chartData = {
          datasets: [
            {
              label: 'Performance',
              data: this.bigLineChart.allData[index]
            }
          ],
          labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        };
        this.bigLineChart.chartData = chartData;
        this.bigLineChart.activeIndex = index;
      },
      async getCountCameras(){
        const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/cameras/");
        return response.data.total_cameras;
      },
      async getCountUsers(){
        const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/total_users/");
        return response.data.total_users;
      },
      async getCountClips(){
        const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/clips/");
        return response.data.total_clips;
      },
      // async getLastChangeUsers(){
      //   const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/historical_users/");
      //   return response.data;
      // },
      async getTotalClipsPerMonth(){
        const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/clips_per_month/");
        return response.data;
      }
    },
    async mounted() {
      try {
        this.loaded = false;
        this.total_cameras =  await this.getCountCameras();
        this.total_users =  await this.getCountUsers();
        this.total_clips = await this.getCountClips();
        //this.last_change_users = await this.getLastChangeUsers();
        const clips_per_month = await this.getTotalClipsPerMonth();
        let count_clips_month_default = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        this.redBarChart.chartData.datasets[0].data = count_clips_month_default.map((x, index)=>{
          const month = index + 1;
          const month_found = clips_per_month.find(element => parseInt(element.month.split('-')[1]) == month);
          if(month_found){
            return month_found.total;
          }
          return x;
        });
        this.loaded = true;
      } catch (error) {
        console.error(error);
      }
      //this.initBigChart(0);
    }
  };
</script>
<style>
.el-table .cell{
  padding-left: 0px;
  padding-right: 0px;
}
</style>
