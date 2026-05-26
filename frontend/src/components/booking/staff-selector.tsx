"use client";

import { motion } from "framer-motion";

type Staff = {
  id: number;
  first_name: string;
  last_name: string;
};

type Props = {
  staff: Staff[];
  selectedStaff: number | null;
  onSelect: (id: number) => void;
};

export default function StaffSelector({
  staff,
  selectedStaff,
  onSelect,
}: Props) {
  return (
    <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      {staff.map((member, index) => {
        const active = selectedStaff === member.id;

        return (
          <motion.button
            key={member.id}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: index * 0.08,
              duration: 0.5,
            }}
            whileHover={{
              y: -4,
            }}
            whileTap={{
              scale: 0.98,
            }}
            onClick={() => onSelect(member.id)}
            className={`
              group relative overflow-hidden rounded-[2rem]
              border p-6 text-right transition-all duration-500
              ${
                active
                  ? "border-[#D4B483] bg-[#D4B483]/10"
                  : "border-white/10 bg-white/[0.03] hover:border-white/20"
              }
            `}
          >
            {/* glow */}
            <div className="absolute inset-0 opacity-0 transition duration-500 group-hover:opacity-100">
              <div className="absolute -top-20 left-1/2 h-40 w-40 -translate-x-1/2 rounded-full bg-[#D4B483]/10 blur-3xl" />
            </div>

            <div className="relative z-10">
              {/* avatar */}
              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-[#D4B483]/15 text-xl font-semibold text-[#D4B483]">
                {member.first_name.charAt(0)}
              </div>

              <h3 className="text-2xl font-semibold">
                {member.first_name} {member.last_name}
              </h3>

              <p className="mt-2 text-sm text-zinc-500">
                متخصص خدمات VIP
              </p>

              <div className="mt-8 flex items-center justify-between">
                <span className="text-sm text-zinc-400">
                  انتخاب متخصص
                </span>

                {active && (
                  <motion.div
                    layoutId="active-staff"
                    className="rounded-full bg-[#D4B483] px-3 py-1 text-xs font-medium text-black"
                  >
                    انتخاب شد
                  </motion.div>
                )}
              </div>
            </div>
          </motion.button>
        );
      })}
    </div>
  );
}