<template>
    <v-container>
        <v-row>
            <v-col>
                <v-select
                        :items="dates"
                        label="Pick a Date"
                        outlined
                        v-model="date"
                ></v-select>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
    export default {
        name: "DateSelector",
        props: ["dates"],
        data() {
            return {
                date: ""
            }
        },
        watch:{
            date(newVal){
                this.$store.commit("SET_DATE_SELECTED", newVal)
            }
        }
    }
</script>
