<template>
    <v-form>
        <v-container>
            <v-row>
                <v-col>
                    <v-text-field
                            label="Location"
                            prepend-icon="mdi-map-marker"
                            v-model="location"
                    ></v-text-field>
                </v-col>
                <v-col align="center" class="pt-6">
                    <v-btn
                            color="primary"
                            x-large
                            @click="submit_location"
                    >
                        Enter
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>

<script>
    export default {
        name: "SearchBar",
        data() {
            return { location:"" }
        },
        methods: {
            async submit_location(){
                if(this.location === ""){
                    this.$store.commit("SET_MODAL_DATA",
                        {
                            isVisible:true,
                            ModalTitle:"EEE!! We need location to proceed :(",
                            ModalInfo:{detail:"Please enter a location"}
                        })
                    return
                }
                this.$store.dispatch('set_location', this.location)

                // Loader appears
                this.$store.commit("TOGGLE_LOADER", true)
                // Fetch info
                await this.$store.dispatch("get_temperature_data", this.location)
                // Loader disappear
                this.$store.commit("TOGGLE_LOADER", false)

            }
        }
    }
</script>

<style scoped>

</style>
