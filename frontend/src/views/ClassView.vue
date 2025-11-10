<template>
<p>Class View</p>
<table> 
<tr v-for="c in classOverview" :key="c.classId" @click="showDetails(c.classId)">
<td>{{ c.classId }}</td><td>{{ c.violationsCount }}</td> </tr> </table>
<table v-if="selected"> 
<tr v-for="e in selected?.examples" :key="e.message"> 
<td>{{ e.node }}</td>
<td>{{ e.path }}</td>
<td>{{ e.message }}</td> </tr> </table>
</template>

<script> 
import { classOverview, classDetails } from "@/mock-data/mock-data"; 
export default { 
    data() { 
        return { classOverview, classDetails, selected: null }; }, 
    methods: { 
        showDetails(id) { 
            this.selected = classDetails(id); }, }, }; 
</script>  

