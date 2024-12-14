<script setup lang="ts">
import PrimaryButton from "@/components/PrimaryButton.vue";
import type { Filtering, Ordering } from "@/components/TableCard.vue";
import TableCard from "@/components/TableCard.vue";
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import type { Class, Room } from "@/types";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";

const classes = ref<Class[]>([]);
const classDescriptions = computed(() =>
  classes.value.map((x) => x.class_description),
);

const rooms = defineModel<Room[]>();

const roomsOrdering = ref<Ordering>();
const roomsFiltering = ref<Filtering>();

watch([roomsOrdering, roomsFiltering], () => {
  fetchRooms();
});

async function fetchClasses() {
  classes.value = (await axios.get("/api/class/")).data;
}

async function fetchRooms() {
  let orderingParam = roomsOrdering.value?.name;
  if (roomsOrdering.value?.order === "descending") {
    orderingParam = `-${orderingParam}`;
  }

  const classFilter = roomsFiltering.value?.room_class;

  rooms.value = (
    await axios.get("/api/room/", {
      params: {
        ordering: orderingParam,
        room_class:
          classFilter === undefined ? undefined : classes.value[classFilter].id,
        status: "notready",
      },
    })
  ).data;
}

async function freeRoom(roomItem: Room) {
  await axios.patch(`/api/room/${roomItem.id}/`, {
    status: "free",
  });
  await fetchRooms();
}

onMounted(async () => {
  await fetchClasses();
  await fetchRooms();
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "cleaning" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <h1 class="pb-2 pt-6 text-center text-4xl font-extrabold lg:text-start">
      Rooms
    </h1>
    <TableCard
      v-model:ordering="roomsOrdering"
      v-model:filtering="roomsFiltering"
      :columns="[
        { name: 'room_number', display: 'Room number', ordering: true },
        { name: 'room_class', display: 'Class', filtering: classDescriptions },
        { name: 'status', display: 'Status' },
      ]"
      :rows="rooms"
    >
      <template #room_number="item">
        <span v-if="!item.isFormRow">{{ item.data.room_number }}</span>
      </template>

      <template #places="item">
        <span v-if="!item.isFormRow">{{ item.data.places }}</span>
      </template>

      <template #room_class="item">
        <span v-if="!item.isFormRow">{{
          classes.find((x) => x.id == item.data.room_class)?.class_description
        }}</span>
      </template>

      <template #status="item">
        <PrimaryButton v-if="!item.isFormRow" @click="freeRoom(item.data)"
          >Set to free</PrimaryButton
        >
      </template>
    </TableCard>
  </main>
</template>
