<script setup lang="ts" generic="T">
import { toRefs } from "vue";
import {
  ChevronUpDownIcon,
  ChevronUpIcon,
  ChevronDownIcon,
} from "@heroicons/vue/24/outline";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";

// TODO: pagination
// TODO: typing could probably be improved (models, generic tuples for props)

export type TableCardSlot<T> =
  | {
      isFormRow: true;
    }
  | {
      isFormRow: false;
      data: T;
    };

export type Column = {
  name: string;
  display: string;
} & (
  | { ordering?: boolean; filtering?: undefined }
  | { ordering?: undefined; filtering?: readonly string[] }
);

export type Ordering = {
  name: string;
  order: "ascending" | "descending";
};

export type Filtering = {
  [column: string]: string;
};

const props = defineProps<{
  columns: Column[];
  rows: readonly T[];
  extraFormRow?: {
    formName: string;
    formSubmit: () => boolean | Promise<boolean>;
  };
}>();

const ordering = defineModel<Ordering>("ordering");
const filtering = defineModel<Filtering>("filtering");

const { columns, rows, extraFormRow } = toRefs(props);

function setOrdering(column: string) {
  if (ordering?.value?.name === column) {
    if (ordering.value.order === "ascending") {
      ordering.value = {
        name: column,
        order: "descending",
      };
    } else {
      ordering.value = undefined;
    }
  } else {
    ordering.value = {
      name: column,
      order: "ascending",
    };
  }
}

function setFiltering(column: string, filter?: string) {
  if (filtering.value === undefined) {
    filtering.value =
      filter !== undefined
        ? {
            [column]: filter,
          }
        : {};
  } else {
    if (filter !== undefined) {
      filtering.value[column] = filter;
    } else {
      delete filtering.value[column];
    }
    filtering.value = Object.assign({}, filtering.value);
  }
}
</script>

<template>
  <div
    class="mt-4 rounded-3xl bg-slate-100 px-0 py-6 text-surface-content-light shadow-md dark:bg-secondary-dark dark:text-surface-content-dark"
  >
    <form
      v-if="extraFormRow !== undefined"
      :id="extraFormRow.formName"
      @submit.prevent="extraFormRow.formSubmit"
    />

    <table
      class="w-full table-auto bg-slate-100 text-center dark:bg-secondary-dark"
    >
      <thead
        class="border-b border-secondary-light dark:border-secondary-active-dark"
      >
        <tr>
          <th v-for="column in columns" v-bind:key="column.name" class="py-2">
            <div
              v-if="column.ordering === true"
              class="flex w-full flex-row justify-center"
            >
              <button
                class="flex flex-row justify-center space-x-1"
                @click="setOrdering(column.name)"
              >
                <span>{{ column.display }}</span>
                <ChevronUpDownIcon
                  v-if="ordering?.name !== column.name"
                  class="w-[24px]"
                />
                <ChevronUpIcon
                  v-else-if="ordering.order === 'ascending'"
                  class="w-[24px]"
                />
                <ChevronDownIcon v-else class="w-[24px]" />
              </button>
            </div>
            <div
              v-else-if="column.filtering !== undefined"
              class="flex w-full flex-row justify-center"
            >
              <Popover class="relative">
                <PopoverButton
                  class="flex flex-col items-center justify-center outline-none"
                  @click="setOrdering(column.name)"
                >
                  <span class="leading-3">{{ column.display }}</span>
                  <ChevronDownIcon class="w-[16px]" />
                </PopoverButton>

                <transition
                  enter-active-class="transition duration-200 ease-out"
                  enter-from-class="translate-y-1 opacity-0"
                  enter-to-class="translate-y-0 opacity-100"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="translate-y-0 opacity-100"
                  leave-to-class="translate-y-1 opacity-0"
                >
                  <PopoverPanel
                    class="absolute left-1/2 z-10 mt-1 -translate-x-1/2"
                  >
                    <div
                      class="flex flex-col overflow-hidden rounded-xl bg-surface-light text-surface-content-light shadow-xl dark:bg-surface-dark dark:text-surface-content-dark"
                    >
                      <button
                        class="py-2"
                        :class="[
                          filtering === undefined ||
                          filtering[column.name] === undefined
                            ? 'bg-primary-active-light text-primary-content-light dark:bg-primary-active-dark dark:text-primary-content-dark'
                            : 'hover:bg-primary-light hover:text-primary-content-light dark:hover:bg-primary-dark dark:hover:text-primary-content-dark',
                        ]"
                        @click="setFiltering(column.name)"
                      >
                        <span class="px-4">None</span>
                      </button>
                      <button
                        v-for="filter in column.filtering"
                        v-bind:key="filter"
                        class="py-2"
                        :class="[
                          filtering !== undefined &&
                          filtering[column.name] === filter
                            ? 'bg-primary-active-light text-primary-content-light dark:bg-primary-active-dark dark:text-primary-content-dark'
                            : 'hover:bg-primary-light hover:text-primary-content-light dark:hover:bg-primary-dark dark:hover:text-primary-content-dark',
                        ]"
                        @click="setFiltering(column.name, filter)"
                      >
                        <span class="px-4">
                          {{ filter }}
                        </span>
                      </button>
                    </div>
                  </PopoverPanel>
                </transition>
              </Popover>
            </div>
            <span v-else>{{ column.display }}</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-surface-light dark:bg-surface-dark">
        <tr v-for="[rowIndex, row] in rows.entries()" v-bind:key="rowIndex">
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot
              :name="column.name"
              v-bind="{ isFormRow: false, data: row } as TableCardSlot<T>"
            ></slot>
          </td>
        </tr>
        <tr>
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot
              :name="column.name"
              v-bind="{ isFormRow: true } as TableCardSlot<T>"
            ></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
