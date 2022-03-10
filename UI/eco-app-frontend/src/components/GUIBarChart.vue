<template>
    <LineChart :chartData="chartData" :options="options" />
</template>

<script>
    import { Chart, registerables} from 'chart.js';
    import { LineChart } from 'vue-chart-3';

    Chart.register(...registerables)

    export default {
        name: "GUIBarChart",
        props: ["chartData", "options"],
        components:{
            LineChart
        }
    }
</script>
