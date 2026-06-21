import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  type RegisterFormData,
  registerSchema,
} from "../services/registerSchema";
import styles from "./LoginForm.module.scss";
import { Link } from 'react-router-dom';

type Props = {
  onSubmit: (
    data: RegisterFormData
  ) => Promise<void>;
};

export default function RegisterForm({
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.field}>
          <label>Email</label>
          <input
            autoComplete="email"
            {...register("email")}
          />
          <p className={styles.error}>
            {errors.email?.message}
          </p>
        </div>
        <div className={styles.field}>
          <label>Password</label>
          <input
            type="password"
            autoComplete="new-password"
            {...register("password")}
          />
          <p className={styles.error}>
            {errors.password?.message}
          </p>
        </div>
        <div className={styles.field}>
          <label>Confirm Password</label>
          <input
            type="password"
            autoComplete="new-password"
            {...register("confirmPassword")}
          />
          <p className={styles.error}>
            {errors.confirmPassword?.message}
          </p>
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Registering..." : "Register"}
        </button>
      </form>
      <div className={styles.register}>
        <p>Already have an account? <Link to="/login">Login here</Link></p>
      </div>
    </>
  );
}
