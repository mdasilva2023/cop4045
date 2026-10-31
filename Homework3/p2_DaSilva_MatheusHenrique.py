"""Homework 3, Problem 2 - Matheus Henrique Da Silva - Z23704669"""


class ParkingPermit:
    """base permit with an owner, duration, and configurable fee schedule."""

    def __init__(self, owner: str, months: int, fees: dict[str, int | float]) -> None:
        """store permit details; months must be nonnegative and fees hold rates."""
        if months < 0:
            raise ValueError("months cannot be negative")
        self.owner = owner
        self.months = months
        self.fees = fees.copy()

    def cost(self) -> float:
        """return permit cost; subclasses must implement their own formula."""
        raise NotImplementedError("Use a specific permit type")

    def __str__(self) -> str:
        """return a readable description of the permit."""
        return f"ParkingPermit(owner={self.owner}, months={self.months})"

    def __repr__(self) -> str:
        """return a detailed representation of the permit."""
        return f"ParkingPermit({self.owner!r}, {self.months!r}, {self.fees!r})"


class StudentPermit(ParkingPermit):
    """student parking permit with a registered vehicle count."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, int | float], vehicles: int) -> None:
        """initialize a student permit; vehicles must be at least one."""
        super().__init__(owner, months, fees)
        if vehicles < 1:
            raise ValueError("vehicles must be at least 1")
        self.vehicles = vehicles

    def cost(self) -> float:
        """return monthly charges plus one-time fees for extra vehicles."""
        return (self.months * self.fees["monthly"]
                + (self.vehicles - 1) * self.fees["extra_vehicle"])

    def __str__(self) -> str:
        """return a readable student permit description."""
        return (f"StudentPermit(owner={self.owner}, months={self.months}, "
                f"vehicles={self.vehicles})")

    def __repr__(self) -> str:
        """return a detailed student permit representation."""
        return (f"StudentPermit({self.owner!r}, {self.months!r}, "
                f"{self.fees!r}, {self.vehicles!r})")


class FacultyPermit(ParkingPermit):
    """faculty parking permit with optional garage access."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, int | float], garage: bool) -> None:
        """initialize a faculty permit with its garage access setting."""
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """return monthly base cost plus monthly garage charges if enabled."""
        return self.months * (self.fees["monthly"]
                              + (self.fees["garage"] if self.garage else 0))

    def __str__(self) -> str:
        """return a readable faculty permit description."""
        return (f"FacultyPermit(owner={self.owner}, months={self.months}, "
                f"garage={self.garage})")

    def __repr__(self) -> str:
        """return a detailed faculty permit representation."""
        return (f"FacultyPermit({self.owner!r}, {self.months!r}, "
                f"{self.fees!r}, {self.garage!r})")


def summarize_list(permits: list[ParkingPermit]) -> float:
    """print each owner's permit cost and return combined revenue."""
    total = 0.0
    for permit in permits:
        amount = permit.cost()
        print(f"{permit.owner}: ${amount:.2f}")
        total += amount
    return total


def main() -> None:
    """show permit construction, printing, costs, and total revenue."""
    student_fees = {"monthly": 25, "extra_vehicle": 10}
    faculty_fees = {"monthly": 40, "garage": 15}

    permits = [
        StudentPermit("Alex", 4, student_fees, 2),
        StudentPermit("Taylor", 2, student_fees, 1),
        FacultyPermit("Jordan", 4, faculty_fees, True),
        FacultyPermit("Morgan", 3, faculty_fees, False),
    ]

    print("Matheus Henrique Da Silva - Z23704669")
    print("Parking permit objects:")
    for permit in permits:
        print(str(permit))
        print(repr(permit))

    print("\nPermit cost summary:")
    total = summarize_list(permits)
    print(f"Total revenue: ${total:.2f}")


if __name__ == "__main__":
    main()
