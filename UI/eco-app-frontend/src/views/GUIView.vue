<template>
    <v-container class="grey lighten-5 mb-12">
        <v-row class="mb-4 mt-4">
            <v-col align="center">
                <v-card class="py-4 pl-2"
                        outlined
                        elevation="6"
                >
                    <h3>Temperature Data Per Location</h3>
                </v-card>
            </v-col>
        </v-row>

        <v-row class="mb-6">
            <v-col>
                <v-card
                        class="pa-2 pt-4"
                        outlined
                        tile
                        elevation="6"
                >
                    <SearchBar></SearchBar>
                </v-card>
            </v-col>
        </v-row>

        <v-row class="mb-6">
            <v-col>
                <v-card
                        outlined
                        tile
                        elevation="6"
                >
                    <DateSelector v-if="unique_dates.length" :dates="unique_dates"></DateSelector>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <v-card
                        outlined
                        tile
                        elevation="6"
                >
                    <GUIBarChart v-if="chartData" :chartData="chartData" :options="get_chart_options()"/>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import GUIBarChart from "@/components/GUIBarChart";
    import SearchBar from "@/components/searchLocation"
    import DateSelector from "@/components/DateSelector";
    import { defineComponent } from 'vue';

    export default defineComponent({
        name: "GUIView",
        components: {
            GUIBarChart,
            SearchBar,
            DateSelector
        },
        methods:{
            get_chart_options(){
                return {
                    plugins: {
                        title: {
                            display: true,
                            text: `Temperature forecast in °C for location ${this.$store.state.location}`
                        }
                    }
                }
            }
        },
        computed: {
            temp_data: {
                get() {
                    return this.$store.state.temperature_data
                }
            },
            data_per_date(){
                let raw_data = this.$store.state.temperature_data
                let temp_by_date = {}
                for(let idx in raw_data){
                    let key_val = raw_data[idx]
                    let key = Object.keys(key_val)[0]
                    let _date = key.split("T")[0]
                    let _hour = key.split("T")[1]
                    if(!(_date in temp_by_date)){
                        temp_by_date[_date] = []
                    }
                    temp_by_date[_date].push([key_val[key],_hour])
                }
                return temp_by_date
            },
            unique_dates(){
                let dates = []
                for(let date_time in this.data_per_date){
                    dates.push(date_time.split("T")[0])
                }
                return dates
            },
            date_selected(){
                return this.$store.state.dateSelected
            },
            chartData(){
                let data_per_date = this.data_per_date
                let date_selected = this.date_selected
                let data = []
                let labels = []

                if(!this.unique_dates.includes(date_selected)){
                    return false
                }
                let raw_data = data_per_date[date_selected]
                for(let idx in raw_data){
                    let [_data, _label] = raw_data[idx]
                    data.push(_data)
                    labels.push(_label)
                }
                return {
                    labels: labels,
                    datasets: [
                        {
                            data: data,
                            backgroundColor:'rgba(172, 192, 182, 1)',
                            label: 'Temperature in °C',
                            borderColor:'',
                            pointBorderWidth:2,
                            pointHitRadius:2,
                            pointRadius:6,
                            pointBorderColor:"rgba(0, 192, 182, 1)"
                        },
                    ],
                };
            }
        }
    });
</script>
